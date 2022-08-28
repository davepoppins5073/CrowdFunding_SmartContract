pragma solidity >=0.7.0 <0.9.0;
contract test{


    function getBytes32() pure public returns (bytes32[2] memory B32Arr){
        B32Arr = [bytes32("proposal1"), bytes32("proposal2")];
    }
}