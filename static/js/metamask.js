//function myFunction() {
//    alert("Hello from a statiddc file!");
    
//}

function web3Login() {
    try {
        window.ethereum.enable().then(function () {
            provider = new ethers.providers.Web3Provider(window.ethereum);
            provider.getNetwork().then(function (result) {
                if (result['chainId'] != 1) {
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
    } catch {
        alert('Please install MetaMask for your browser.')
    }
}

function web3LoginBackend(accountAddress, signature) {
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
