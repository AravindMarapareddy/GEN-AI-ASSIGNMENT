async function sendMessage(){

let message = document.getElementById("message").value

let chatbox = document.getElementById("chatbox")

chatbox.innerHTML += "<p><b>You:</b> " + message + "</p>"

let response = await fetch("/api/chat",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
sessionId:"123",
message:message
})
})

let data = await response.json()

chatbox.innerHTML += "<p><b>Bot:</b> " + data.reply + "</p>"

}