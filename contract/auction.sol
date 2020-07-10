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

    constructor() public {                  
        items[0] = itemDescription({size: 9, duration: 2, price: 80});
        //items[1] = itemDescription({size: 11, duration: 2, price: 100});
        //items[2] = itemDescription({size: 13, duration: 2, price: 120});
        
        bids[0] = itemDescription({size: 8, duration: 2, price: 90});
        //bids[1] = itemDescription({size: 10, duration: 2, price: 150});
        //bids[2] = itemDescription({size: 12, duration: 2, price: 200});
        
        X.push(0);
        //X.push(1);
        //X.push(2);
        
        prices.push(85);//correct price
        //prices.push(90);//in correct price (lower than the reservation price)
        //prices.push(15);//in correct price (higher than the reservation price)
        
        score = 140;
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
