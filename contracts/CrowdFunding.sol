// SPDX-License-Identifier: MIT

pragma solidity >=0.6.6 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.7/vendor/SafeMathChainlink.sol";

contract Crowdfunding {
    // This is to avoid overflow in the older versions (less than version 8).
    using SafeMathChainlink for uint256;
    
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    // fundraiser / owner / admin : 
    address public owner;
 
    // constructor gets called when the smart contract gets deployed 
    constructor() public {
        owner = msg.sender;
    }
      
    function fund() public payable {
        uint256 minimumUSD = 1 * 10 ** 18;
        require(getConversionRate(msg.value) >= minimumUSD, "You need to spend more ETH!");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }
    
    function getVersion() public view returns (uint256){
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
        return priceFeed.version();
    }
    
    function getPrice() public view returns(uint256){
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
        (,int256 answer,,,) = priceFeed.latestRoundData();
         return uint256(answer * 10000000000);
    }
    
    // 1000000000
    function getConversionRate(uint256 ethAmount) public view returns (uint256){
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }
    
    modifier onlyOwner {
        // only want the contract admin/owner to withdraw money 
        require(msg.sender == owner,"invalid funder try to withdraw money");
        _;
    }

    function withdraw() payable onlyOwner public {
       payable(msg.sender).transfer(address(this).balance); 
       for(uint256 funderIndex=0; funderIndex < funders.length; funderIndex++){
           address funder = funders[funderIndex];
           addressToAmountFunded[funder] = 0; 
       }
       funders = new address[](0);
    }    
}
