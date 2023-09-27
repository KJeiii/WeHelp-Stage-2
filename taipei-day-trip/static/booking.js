async function createItinerary () {
    let itineraryInfo = {
        "user_id": 6,
        "attraction_id": 22,
        "date": "2023-10-10",
        "time": "afternoon",
        "price": 2500
    };


    let response = fetch("/api/booking",{
        method: "POST",
        headers: {
            "authorization": `Bearer ${}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(itineraryInfo)
        })
}

