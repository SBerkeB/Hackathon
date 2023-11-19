


document.getElementById("connect_button").addEventListener("click", async () => {
    const acc = await window.ethereum.request({ method: "eth_requestAccounts" });
    console.log(acc[0]);
})