window.sendMessage = async function() {

    const input =
        document.getElementById(
            "messageInput"
        );

    const chatBox =
        document.getElementById(
            "chatBox"
        );

    const message =
        input.value.trim();

    if (!message) {
        return;
    }

    chatBox.innerHTML += `
        <div>
            <b>You:</b>
            ${message}
        </div>
        <hr>
    `;

    input.value = "";

    const response =
        await fetch(
            "/chat",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    message: message
                })
            }
        );

    const data =
        await response.json();

    chatBox.innerHTML += `
        <div>
            <b>Assistant:</b>
            ${data.answer}
        </div>
        <hr>
    `;

    chatBox.scrollTop =
        chatBox.scrollHeight;
}