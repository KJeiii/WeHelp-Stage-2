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
            "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2kiOjYsInVzbiI6IjEyMyIsImVtbCI6IjEyM0BtYWlsIiwiZXhwIjoxNjk2NDI3NzExLCJpYXQiOjE2OTU4MjI5MTF9.hY0qUQhhLxY-GX-MW-JjH0nkpr7k9w6p8mBm2L4keEA",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(itineraryInfo)
        })
}

