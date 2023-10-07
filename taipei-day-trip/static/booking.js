// ----- booking function -----
// async function createItinerary () {
//     let itineraryInfo = {
//         "user_id": 6,
//         "attraction_id": 22,
//         "date": "2023-10-10",
//         "time": "afternoon",
//         "price": 2500
//     };

//     try{
//         let response = await fetch("/api/booking",{
//             method: "POST",
//             headers: {
//                 "authorization": `Bearer ${window.localStorage.getItem("token")}`,
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify(itineraryInfo)
//             });
//     }
//     catch(error) {
//         console.log(error);
//     };        
// };

var itineraryInfo=null;

function loadPage() {
    SignStatus()
        .then((result) => {
            if (result["ok"] === true) {
                let welceomMsg = document.querySelector(".welcomeMsg");
                welceomMsg.textContent = `您好，${result["data"]["name"]}，待預訂的行程如下：`;

                fetch("api/booking", {
                    method: "GET",
                    headers: {
                        "authorization": `Bearer ${window.localStorage.getItem("token")}`
                    }
                })
                    .then((response) => {return response.json();})
                    .then((data) => {
                        //parse itinerary information from response body
                        itineraryInfo = data["data"];

                        if (itineraryInfo !== null) {
                            // query all html elements need to be modified
                            let//
                            image = document.querySelector("figure"),
                            itineraryTitle = document.querySelector(".itinerary-title"),
                            itineraryValues = document.querySelectorAll(".itinerary-value"),
                            date = itineraryValues[0],
                            time = itineraryValues[1],
                            fee = itineraryValues[2],
                            address = itineraryValues[3],
                            contactName = document.querySelector("input[name=contact-name]"),
                            contactEmail = document.querySelector("input[name=contact-email]"),
                            totalPrice = document.querySelector(".checkbill-inner p");
                
                            // modify html elements
                            image.style.backgroundImage = `url(${itineraryInfo["attraction"]["image"]})`;
                            itineraryTitle.textContent = `台北一日遊：${itineraryInfo["attraction"]["name"]}`;
                            date.textContent = itineraryInfo["date"];
                                if (itineraryInfo["time"] === "beforenoon") {
                                    time.textContent = "早上9點到下午4點"
                                }
                                else{
                                    time.textContent = "下午4點到下午9點";
                                };
                                fee.textContent = `新台幣${itineraryInfo["price"]}元`;
                                address.textContent = itineraryInfo["attraction"]["address"];
                                contactName.value = result["data"]["name"];
                                contactEmail.value = result["data"]["email"];
                                totalPrice.textContent = `總價：新台幣${itineraryInfo["price"]}元`;
                        }
                        else{
                            let// 
                            itineraryDiv = document.querySelector(".itinerary"),
                            bottomSection = document.querySelector(".bottomSection"),
                            noItinerary = document.createElement("p"),
                            itineraryInner = document.querySelector(".itinerary-inner");
                            itineraryDiv.style.display = "none";
                            bottomSection.style.display = "none";
                            noItinerary.textContent = "目前沒有任何待預訂的行程";
                            noItinerary.setAttribute("class", "no-itinerary");
                            itineraryInner.appendChild(noItinerary);
                        };
                    })
                    .catch(error => {console.log(error)});
            }
            else {window.location.replace("/")};
    })
};

loadPage();

async function deleteItinerary() {
    SignStatus()
        .then((result) => {
            if (result["ok"] === true) {
                fetch("api/booking", {
                    method: "DELETE",
                    headers: {
                        "authorization": `Bearer ${window.localStorage.getItem("token")}`
                    }
                })
                    .then(res => {
                        window.location.replace(window.location.href);
                        return res.json()})
                    .then(data => {console.log(data)})
                    .catch(error => {console.log(error)})
            };
        })
        .catch(error => {console.log(error)});
};

// ----- credit card tap pay SDK -----
// set up SDK
TPDirect.setupSDK(
    appID = 137169,
    appKey = "app_mb6V0dG1tbb6uz1CEVeP1uHHbleFJ8fRSqRnK64N2jL4PeLcx5BJwMicNA7i",
    serverType = "sandbox"
);

// set up html input
let fields = {
    number: {
        element: "#card-number",
        placeholder: "**** **** **** ****"
    },
    expirationDate: {
        element: "#card-expiration-date",
        placeholder: "MM / YY"
    },
    ccv: {
        element: "#card-ccv",
        placeholder: "後三碼"
    }
};

TPDirect.card.setup({
    fields: fields,
    styles: {
        "input": {
            "width": "180px",
            "height": "10px",
            "padding": "10px",
            "border-radius": "5px",
            "border": "1px solid #e8e8e8",
            "font-size": "16px",
            "font-style": "normal",
            "font-weight": "500",
            "color": "#000"
        }}
});

// POST payment information
function checkBill() {
    SignStatus()
        .then(res => {
            console.log(TPDirect.paymentRequestApi.checkAvailability());
            if (res["ok"] === true) {
                let TPfieldsStatus = TPDirect.card.getTappayFieldsStatus();
                if ( TPfieldsStatus.canGetPrime === true) {
                    TPDirect.card.getPrime(result => {
            
                        // orgainze order info for database storage
                        let orderInfo = {
                            "prime": result.card.prime,
                            "order": {
                                "price": itineraryInfo["price"],
                                "trip": {
                                    "attraction": {
                                        "id": itineraryInfo["attraction"]["id"],
                                        "name": itineraryInfo["attraction"]["name"],
                                        "address": itineraryInfo["attraction"]["address"],
                                        "image": itineraryInfo["attraction"]["image"]
                                    },
                                    "date": itineraryInfo["date"],
                                    "time": itineraryInfo["time"]}},
                            "contact": {
                                "name": res["data"]["name"],
                                "email": res["data"]["email"],
                                "phone": document.querySelector("input[name=contact-phone]").value}
                            }
                            // console.log(orderInfo);

                        // POST info
                        fetch("/api/orders", {
                            method: "POST",
                            headers: {
                                "Authorization": `Bearer ${window.localStorage.getItem("token")}`,
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify(orderInfo)
                        })
                            .then(res => {return res.json()})
                            .then(result => {
                                console.log(result)
                                window.location.replace(`/thankyou?number=${result["data"]["number"]*1}`)
                            })
                            .catch(err => {console.log(err)})
                    });
                }
            }
        })
        .catch(error => {console.log(error)})
};

