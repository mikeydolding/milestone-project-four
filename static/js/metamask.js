window.addEventListener("DOMContentLoaded", () => {
  const onboarding = new MetaMaskOnboarding();
  const onboardButton = document.getElementById("onboard");
  const showAccountDesc = document.querySelector(".showAccount");
  const chainElement = document.getElementById("chain");
  const errorElement = document.getElementById("error");

  let accounts;

//  // + Display the selected wallet address
//const showAccount = () => {
//  console.log('showAccount')
//    showAccountDesc.innerHTML = 'Account: ' + accounts[0];
//}
//// + Displays an error to the user when trying to connect the wallet
//const showError = (err) => {
//  console.log('error')
//  errorElement.textContent = err.message;
//}
  const updateButton = () => {
    if (!MetaMaskOnboarding.isMetaMaskInstalled()) {
      onboardButton.innerText = "Click here to install MetaMask!";
      onboardButton.onclick = () => {
        onboardButton.innerText = "Onboarding in progress";
        onboardButton.disabled = true;
        onboarding.startOnboarding();
      };
    } else if (accounts && accounts.length > 0) {
      onboardButton.innerText = "Connected";
      onboardButton.disabled = true;
      onboarding.stopOnboarding();
      showAccountDesc.innerHTML = accounts[0];
    } else {
      onboardButton.innerText = "Connect";
      onboardButton.onclick = async () => {
        alert('connect')
        //window.ethereum.enable()
        //await window.ethereum.request({
        //  method: "eth_requestAccounts",
        //});
        window.ethereum.enable().then(function () {
          provider = new ethers.providers.Web3Provider(window.ethereum);
          provider.getNetwork().then(function (result) {
            console.log('result',result)
              if (result['chainId'] != 1337) {
                  alert('Switch to Mainnet!');
              } else { 
                  provider.listAccounts().then(function (result) {
                      accountAddress = result[0]; 
                      signer = provider.getSigner();
                      signer.signMessage("Sign to auth {{ csrf_token }}").then((signature) => {web3LoginBackend(accountAddress, signature)});
                  })
              }
          })
      })
      };
    }
  };

  updateButton();
  if (MetaMaskOnboarding.isMetaMaskInstalled()) {
    window.ethereum.on("accountsChanged", (newAccounts) => {
      accounts = newAccounts;
      updateButton();
    });
  }
});

function web3LoginBackend(accountAddress, signature) {
  alert(accountAddress)
  alert(signature)

  var form = document.createElement('form');
  form.action = '{% url "main:auth_web3" %}'; 
  form.method = 'POST';

  var input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'csrfmiddlewaretoken';
  input.value = '{{ csrf_token }}';
  form.appendChild(input);    

  var input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'accountAddress';
  input.value = accountAddress;
  form.appendChild(input);

  var input = document.createElement('input');
  input.type = 'hidden';
  input.name = 'signature';
  input.value = signature;
  form.appendChild(input);

  document.body.appendChild(form);
  form.submit();
}
