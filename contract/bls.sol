pragma solidity ^0.4.23;
pragma experimental ABIEncoderV2;

contract BLS {

  event Issue(uint indexed x, uint indexed y);

  // print out
  event PrintG1Point(uint indexed x, uint indexed y);
  event PrintAddress(address indexed addr);
  event PrintBytes(bytes indexed message);
  event PrintString(string indexed addr);

  struct G1Point {
    uint X;
    uint Y;
  }
  struct G2Point {
    uint[2] X;
    uint[2] Y;
  }

  G2Point pk;
  uint timeout;
  uint id;
  mapping (uint256 => bool) public spentList;

  constructor(G2Point memory _pk, uint _timeout, uint _id) public {
    // TODO: set timer
    pk = _pk;
    timeout = _timeout;
    id = _id;
  }

  /// @return the generator of G1
  function G1Gen() internal returns (G1Point memory) {
      return G1Point(1, 2);
  }

  /// @return the generator of G2
  function G2Gen() internal returns (G2Point memory) {
    return G2Point(
      [11559732032986387107991004021392285783925812861821192530917403151452391805634,
      10857046999023057135944570762232829481370756359578518086990519993285655852781],

      [4082367875863433681332203403145435568316851327593401208105741076214120093531,
      8495653923123431417604973247489272438418190587263600148770280649306958101930]
    );
  }

  function printer(bytes memory message, uint sk) payable public returns (bool) {
    G1Point memory h = hashToG1(message);
    G1Point memory s = mul(h, sk);
    emit PrintG1Point(s.X, s.Y);
    emit PrintBytes(message);
    emit PrintAddress(msg.sender);
    emit PrintG1Point(msg.value, 0);
    //emit PrintString(toString(msg.sender));
    //emit PrintString(toString(message, 22));
    return true;
  }

  function toString(address x) public returns (string memory) {
    bytes memory b = new bytes(20);
    for (uint i = 0; i < b.length; i++)
      b[i] = byte(uint8(uint(x) / (2**(8*(19 - i)))));
    return string(b);
  }

  function verify(bytes memory message, G1Point memory signature) public returns (bool) {
    G1Point memory h = hashToG1(message);
    return pairing2(negate(signature), G2Gen(), h, pk);
  }

  function commit(G1Point memory hTilde) payable public returns (bool) {
    if (msg.value != 0) return false; // set amount to pay here
    if (timeout < now) return false;
    emit Issue(hTilde.X, hTilde.Y);
    return true;
  }

  function reveal(bytes memory message, G1Point memory signature)  public returns (bool) {
    // TODO: check that the addr included in the message matches msg.sender
    // TODO: check that the id included in the message matches the auction id
    uint256 k = bytesToUint(message);
    if (spentList[k]) return false;
    spentList[k] = true;
    return verify(message, signature);
  }

  function bytesToUint(bytes memory b) public returns (uint256){
    // NOTE: can be done in assembly to save gas
    uint256 number;
    for (uint i = 0; i < b.length; i++){
      number = number + uint(b[i])*(2**(8*(b.length-(i+1))));
    }
    return number;
  }


  /// @return the result of computing the pairing check
  /// e(p1[0], p2[0]) *  .... * e(p1[n], p2[n]) == 1
  /// For example pairing([P1(), P1().negate()], [P2(), P2()]) should
  /// return true.
  function pairing(G1Point[] memory p1, G2Point[] memory p2) internal returns (bool) {
      require(p1.length == p2.length);
      uint elements = p1.length;
      uint inputSize = elements * 6;
      uint[] memory input = new uint[](inputSize);

      for (uint i = 0; i < elements; i++)
      {
          input[i * 6 + 0] = p1[i].X;
          input[i * 6 + 1] = p1[i].Y;
          input[i * 6 + 2] = p2[i].X[0];
          input[i * 6 + 3] = p2[i].X[1];
          input[i * 6 + 4] = p2[i].Y[0];
          input[i * 6 + 5] = p2[i].Y[1];
      }

      uint[1] memory out;
      bool success;

      assembly {
          success := call(sub(gas, 2000), 8, 0, add(input, 0x20), mul(inputSize, 0x20), out, 0x20)
      // Use "invalid" to make gas estimation work
          switch success case 0 {invalid()}
      }
      require(success);
      return out[0] != 0;
  }

  /// Convenience method for a pairing check for two pairs.
  function pairing2(G1Point memory a1, G2Point memory a2, G1Point memory b1, G2Point memory b2) internal returns (bool) {
    G1Point[] memory p1 = new G1Point[](2);
    G2Point[] memory p2 = new G2Point[](2);
    p1[0] = a1;
    p1[1] = b1;
    p2[0] = a2;
    p2[1] = b2;
    return pairing(p1, p2);
  }

  function hashToG1(bytes memory message) internal returns (G1Point memory) {
    uint256 h = uint256(keccak256(message));
    return mul(G1Gen(), h);
  }

  function modPow(uint256 base, uint256 exponent, uint256 modulus) internal returns (uint256) {
    uint256[6] memory input = [32, 32, 32, base, exponent, modulus];
    uint256[1] memory result;
    assembly {
        if iszero(call(not(0), 0x05, 0, input, 0xc0, result, 0x20)) {
            revert(0, 0)
        }
    }
    return result[0];
  }

  /// @return the negation of p, i.e. p.add(p.negate()) should be zero.
  function negate(G1Point memory p) internal returns (G1Point memory) {
    // The prime q in the base field F_q for G1
    uint q = 21888242871839275222246405745257275088696311157297823662689037894645226208583;
    if (p.X == 0 && p.Y == 0)
        return G1Point(0, 0);
    return G1Point(p.X, q - (p.Y % q));
  }

  /// @return the sum of two points of G1
  function add(G1Point memory p1, G1Point memory p2) internal returns (G1Point memory r) {
    uint[4] memory input;
    input[0] = p1.X;
    input[1] = p1.Y;
    input[2] = p2.X;
    input[3] = p2.Y;
    bool success;
    assembly {
        success := call(sub(gas, 2000), 6, 0, input, 0xc0, r, 0x60)
    // Use "invalid" to make gas estimation work
        switch success case 0 {invalid()}
    }
    require(success);
  }

  /// @return the product of a point on G1 and a scalar, i.e.
  /// p == p.mul(1) and p.add(p) == p.mul(2) for all points p.
  function mul(G1Point memory p, uint s) internal returns (G1Point memory r) {
    uint[3] memory input;
    input[0] = p.X;
    input[1] = p.Y;
    input[2] = s;
    bool success;
    assembly {
        success := call(sub(gas, 2000), 7, 0, input, 0x80, r, 0x60)
    // Use "invalid" to make gas estimation work
        switch success case 0 {invalid()}
    }
    require(success);
  }
}
