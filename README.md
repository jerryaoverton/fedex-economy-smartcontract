# fedex-economy-smartcontract
The smart contract is a Python/Flask web service running on Heroku. We have written a version of the smart contract in both Python/Flask and Solidity. In production, we'll deploy the smart contract as solidity code running on the live [Etherium](https://www.coindesk.com/learn/ethereum-101/what-is-ethereum) block chain. For demonstration, we deployed the smart contract as a web service to avoid the cost and complication of running on a live block chain network.

The smart contract automatically enforces the rules of the FedEx Economy. It determines how to create and distribute FeX tokens. It keeps track of service providers, service consumers and the FeX balances of everyone participating in the FedEx Economy. The drone interacts directly with the smart contract to take on delivery jobs and hire technicians for maintenance. Human users interact with the smart contract through the [marketplace website](https://fedex-economy-market.herokuapp.com/).
