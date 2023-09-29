// open member page 
function Member () {
    let memberOuter = document.querySelector(".memberOuter");
    memberOuter.style.display = "flex";
};

// switch to SignIn page 
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

// switch to SignUp page 
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

// leave member page
function Close () {
    let memberOuter = document.querySelector(".memberOuter");
    memberOuter.style.display = "none";

    let//
    messageDiv = document.querySelector(".message");
    if (messageDiv !== null) {
        let memberDiv = document.querySelector(".memberDiv");
        memberDiv.removeChild(messageDiv);
    };
}

// new member registration
async function SignUp () {
    let// 
    user_name = document.querySelector(".signup_user_name").value,
    email = document.querySelector(".signup_email").value,
    password = document.querySelector(".signup_password").value,
    SignUpInfo = {
        "user_name": user_name,
        "email": email,
        "password": password
    };

    let messageDiv = document.querySelector(".message");
    if (messageDiv !== null) {
        let memberDiv = document.querySelector(".memberDiv");
        memberDiv.removeChild(messageDiv);
    };

    try {
        let response = await fetch("/api/user",{
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(SignUpInfo)
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

// member sign in
async function SignIn () {
    let// 
    email = document.querySelector(".signin_email").value,
    password = document.querySelector(".signin_password").value,
    SignInInfo = {
        "email": email,
        "password": password
    };

    let messageDiv = document.querySelector(".message");
    if (messageDiv !== null) {
        let memberDiv = document.querySelector(".memberDiv");
        memberDiv.removeChild(messageDiv);
    };

    try {
        let response = await fetch("/api/user/auth",
        {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(SignInInfo)
        });
        let result = await response.json();

        if (response.status === 200) {
            let token = result["token"];
            window.localStorage.setItem("token", token);

            // redirect
            let currentPage = window.location.href;
            window.location.replace(currentPage);
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
};

// check sign status
async function SignStatus() {
    let token = window.localStorage.getItem("token");
    if (token !== null) {
        try {
            let response = await fetch("/api/user/auth", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "authorization": `Bearer ${token}`
                }
            });

            let// 
            data = await response.json(),
            member_info = await data["data"];
            // console.log(member_info);
            
            if (member_info !== null) {
                let//
                signDiv = document.querySelector(".topDiv-navbar-sign"),
                signOutDiv = document.querySelector(".topDiv-navbar-signout");
                signDiv.style.display = "none";
                signOutDiv.style.display = "block";

                let result = {
                    "ok": true,
                    "data": {
                        "id": member_info["id"],
                        "name": member_info["name"],
                        "email": member_info["email"]
                    } 
                }
                return result
            };

            let result = {
                "ok": false,
                "data": null
            }
            return result
        }
        catch(error) {
            console.log(error);
        }
    };
    let result = {
        "ok": false,
        "data": null
    }
    return result
};

// launch SignStatus function at each page loading
SignStatus();

// member sign out
function SignOut() {
    window.localStorage.removeItem("token");

    let currentPage = window.location.href;
    window.location.replace(currentPage);
};

