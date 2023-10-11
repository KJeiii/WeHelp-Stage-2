function loadPage() {
    SignStatus()
        .then((result) => {
            if (result["ok"] === true) {
                let welceomMsg = document.querySelector(".welcomeMsg");
                welceomMsg.textContent = `您好，${result["data"]["name"]}，感謝您的購買，您購買的行程如下：`;

                let orderNumber = window.location.search.split("=")[1]*1

                fetch(`api/order/${orderNumber}`, {
                    method: "GET",
                    headers: {
                        "authorization": `Bearer ${window.localStorage.getItem("token")}`
                    }
                })
                    .then((response) => {return response.json();})
                    .then((data) => {
                        //parse itinerary information from response body
                        let orderInfo = data["data"];
                        console.log(orderInfo);

                        // Redirect to homepage without order created
                        if (orderInfo === null) {
                            window.location.replace("/")
                            return
                        }

                        // query all html elements need to be modified
                        let//
                        image = document.querySelector("figure"),
                        itineraryTitle = document.querySelector(".itinerary-title"),
                        itineraryValues = document.querySelectorAll(".itinerary-value"),
                        dateAndTime = itineraryValues[0],
                        address = itineraryValues[1],
                        fee = itineraryValues[2],
                        number = itineraryValues[3],
                        paymentStatus = itineraryValues[4]
            
                        // modify html elements
                        image.style.backgroundImage = `url(${orderInfo["trip"]["attraction"]["image"]})`;
                        itineraryTitle.textContent = `台北一日遊：${orderInfo["trip"]["attraction"]["name"]}`;
                        dateAndTime.textContent = `${orderInfo["trip"]["date"]} 早上9點到下午4點`;
                        fee.textContent = `新台幣${orderInfo["price"]}元`;
                        address.textContent = orderInfo["trip"]["attraction"]["address"];
                        number.textContent = orderNumber;
                        paymentStatus.textContent = "未付款"

                        if (orderInfo["trip"]["time"] === "afternoon") {
                            dateAndTime.textContent = `${orderInfo["trip"]["date"]} 下午4點到下午9點`
                        }

                        if (orderInfo["status"] === 0) {
                            paymentStatus.textContent = "已付款"
                        }
                    })
                    .catch(error => {console.log(error)});
            }
            else {window.location.replace("/")};
    })
};

loadPage();