const { ethers } = require("ethers"); // ethers 5.7.0

const provider = new ethers.providers.JsonRpcProvider(
  "https://sepolia-rpc.scroll.io/"
);

const signer = new ethers.Wallet(
  "0202ff323cfa5ebeeb5fa70e28dd3cb0a647ecde5a458f21d3a70ead3e2adf1d",
  provider
);

const ABI = [
  "function owner() view returns (address)",
  "function getBuyPrice(address sharesSubject, uint256 amount) view returns (uint256)",
  "function getSellPrice(address sharesSubject, uint256 amount) view returns (uint256)",
  "function sharesBalance(address account, address sharesSubject) view returns (uint256)",
  "function buyShares(address shareSubject,uint256 amount)",
  "function sellShares(address shareSubject,uint256 amount)",
];
let address = "0x93D8E9B878A8C150a94C42D69908D3AF47028665"; //bizim kontrat;
let amount = "10000000000000000"
const contract = new ethers.Contract(address, ABI, provider);

const main1 = async () => {
  const price = await contract.getBuyPrice(address, 1);
  console.log(ethers.utils.formatEther(price));
};

main1();

const main2 = async () => {
  const balance = await contract.sharesBalance(address, address);
  console.log(balance);
  if (balance == 0) {
    return 0;
  }
  const price = await contract.getSellPrice(address, 1);
  console.log(ethers.utils.formatEther(price));
};

main2();
const main3 = async () => {
  let gas = await provider.getGasPrice();
  const overrides = {
    gasLimit: 2000000, // Set an appropriate gas limit
    gasPrice: ethers.utils.parseUnits(gas.toString(), 'wei'), // Set an appropriate gas price
  };
  await contract.connect(signer).buyShares(address, 1, overrides);
};
main3();

const main4 = async () => {
  let gas = await provider.getGasPrice();
  const overrides = {
    gasLimit: 2000000, // Set an appropriate gas limit
    gasPrice: ethers.utils.parseUnits(gas.toString(), 'wei'), // Set an appropriate gas price
  };
  await contract.connect(signer).sellShares(address, 1, overrides);
};
main4();
