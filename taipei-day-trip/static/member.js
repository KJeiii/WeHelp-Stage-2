function Member () {
    let memberOuter = document.querySelector(".memberOuter");
    memberOuter.style.display = "flex";
};

function SignInSwitch () {
    let//
    Singup = document.querySelector(".memberDiv-Signup"),
    Signin = document.querySelector(".memberDiv-Signin");
    Singup.style.display = "none";
    Signin.style.display = "block";

    let//
    messageDiv = document.querySelector(".message");
    if (messageDiv !== null) {
        let memberDiv = document.querySelector(".memberDiv");
        memberDiv.removeChild(messageDiv);
    };
};

function SignUpSwitch () {
    let//
    Singup = document.querySelector(".memberDiv-Signup"),
    Signin = document.querySelector(".memberDiv-Signin");
    Singup.style.display = "block";
    Signin.style.display = "none";

    let//
    messageDiv = document.querySelector(".message");
    if (messageDiv !== null) {
        let memberDiv = document.querySelector(".memberDiv");
        memberDiv.removeChild(messageDiv);
    };
};

function Cancel () {
    let memberOuter = document.querySelector(".memberOuter");
    memberOuter.style.display = "none";
}

async function SignUp () {
    let// 
    user_name = document.querySelector(".signup_user_name").value,
    email = document.querySelector(".signup_email").value,
    password = document.querySelector(".signup_password").value,
    data = {
        "user_name": user_name,
        "email": email,
        "password": password
    };

    try {
        let response = await fetch("/api/user",{
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
            });
        let result = await response.json();

        if (response.status === 200) {
            let// 
            message = "註冊成功",
            messageDiv = document.createElement("div"),
            memberDiv = document.querySelector(".memberDiv");

            messageDiv.setAttribute("class", "message");
            messageDiv.textContent = message;
            memberDiv.appendChild(messageDiv);
        };

        let// 
        message = result["message"],
        messageDiv = document.createElement("div"),
        memberDiv = document.querySelector(".memberDiv");

        messageDiv.setAttribute("class", "message");
        messageDiv.textContent = message;
        messageDiv.style.color = "red";
        memberDiv.appendChild(messageDiv);
    }
    catch(error) {
        console.log(error);
    };
}