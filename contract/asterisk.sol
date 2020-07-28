pragma solidity ^0.5.1;

contract asterisk {

    struct itemDescription {
        uint size;
        uint duration;
        uint price;
    }


    mapping(uint => itemDescription) public bids;
    mapping(uint => itemDescription) public items;

    uint[] public X;
    //indexed by bidID
    uint[] public prices;
    int public score;
    uint public highestScore = 0;
    uint depositLimit = 100;
    uint deposit = 0;
    uint itemCounter = 0;
    uint bidsCounter = 0;

    constructor() public {

    }


    function submitBid(uint size, uint duration, uint price) public returns(uint) {
        bidsCounter++;
        bids[bidsCounter] = itemDescription({size: size, duration: duration, price: price});
        return bidsCounter;
    }


    function submitSolution(uint[] memory X_, uint[] memory prices_, uint score_) public payable {
        if((score_ > highestScore && msg.value >= depositLimit)){
            X = X_;
            prices = prices_;
            score = int(score_);
            deposit = msg.value;
            highestScore=score_;
        }
    }

    function addItem(uint size, uint duration, uint price) public returns(uint){
        itemCounter++;
        items[itemCounter] = itemDescription({size: size, duration: duration, price: price});
        return itemCounter;
    }


    function  deriveNetEvaluation(uint bidID, uint itemID) view public returns (uint) {

        itemDescription memory bid = bids[bidID];
        itemDescription memory item =  items[itemID];

        if((item.size >= bid.size) && (item.duration >= bid.duration)){
            int diff= int(bid.price - prices[itemID]);
            if(diff > 0)
                return  uint(diff);
        }
        return 0;

    }

    function calculateScore()view public returns (uint){
        uint sum = 0;
        for (uint i=0; i<X.length; i++) {
            sum += deriveNetEvaluation(i, X[i]);
        }
        return sum;
    }

    function wrongScore() public returns (bool){
        if(calculateScore() != uint(score)){
            score = 0;
            return true;
        }
        return false;
    }

    function wrongAssignment(uint bidID, uint alternativeItemID) public returns (bool){
        uint currentProfit = deriveNetEvaluation(bidID, X[bidID]);
        uint alternativeProfit = deriveNetEvaluation(bidID, alternativeItemID);

        if(currentProfit < alternativeProfit){
            score = -1;
            msg.sender.transfer((deposit * 8) / 10);
            return true;
        }
        return false;
    }

    function wrongPrice(uint bidID) public returns (bool){
        uint contestedPrice = prices[bidID];
        if( (contestedPrice > bids[bidID].price) || (contestedPrice < items[X[bidID]].price) ){
            score = -1;
            return true;
        }
        return false;
    }
}
