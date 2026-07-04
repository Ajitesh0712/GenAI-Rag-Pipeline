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

    <div class="message user-message">

        <div class="message-content">

            ${message}

        </div>

    </div>

    `;

    input.value = "";

    const response =
        await fetch(
            "/chat-stream",
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

    const reader = response.body.getReader();

        const decoder = new TextDecoder();

        let answer = "";

        const assistantMessage = document.createElement("div");

        assistantMessage.className = "message assistant-message";

        assistantMessage.innerHTML = `

        <div class="message-content">

            <div class="assistant-title">

                <div class="assistant-avatar">

                    <i class="bi bi-stars"></i>

                </div>

                AI Assistant

            </div>

            <div class="streaming-answer mt-3"></div>

        </div>

        `;

        chatBox.appendChild(
            assistantMessage
        );

const answerDiv =
    assistantMessage.querySelector(
        ".streaming-answer"
    );
        let buffer = "";

        while (true) {

            const { done, value } =
                await reader.read();

            if (done) {
                break;
            }

            buffer += decoder.decode(
                value,
                {
                    stream: true
                }
            );

            const lines = buffer.split("\n");

            buffer = lines.pop();

            for (const line of lines) {

                if (!line.trim()) {
                    continue;
                }

                const event = JSON.parse(line);

                if (event.type === "token") {

                    answer += event.content;

                    answerDiv.innerHTML =
                        marked.parse(answer);

                }

                else if (event.type === "sources") {

                    let sourcesHTML = `

                        <div class="sources">

                            <strong>📄 Sources</strong><br>

                    `;

                    event.content.forEach(source => {

                        sourcesHTML += `

                            <span class="source-chip">

                                ${source.filename}

                            </span>

                        `;

                    });

                    sourcesHTML += "</div>";

                    answerDiv.innerHTML += sourcesHTML;

                }

                else if (event.type === "done") {

                    console.log("Streaming Finished");

                }

                chatBox.scrollTop =
                    chatBox.scrollHeight;

            }

        }
    }

window.uploadDocument = async function() {
    
    const fileInput =
        document.getElementById(
            "fileInput"
        );

    if (
        fileInput.files.length === 0
    ) {
        alert("Select a file");
        return;
    }

    const formData =
        new FormData();

    formData.append(
        "file",
        fileInput.files[0]
    );

    const response =
        await fetch(
            "/upload",
            {
                method: "POST",
                body: formData
            }
        );

    const data =
        await response.json();

    if (!response.ok) {

        alert(data.detail);

        return;

    }

    document.getElementById(
        "uploadStatus"
    ).innerHTML =
        `Indexed ${data.chunks} chunks from ${data.filename}`;
        await window.loadDocuments();
}



window.loadDocuments = async function () {

    const response = await fetch("/documents");

    const data = await response.json();

    const container =
        document.getElementById("documentsList");

    container.innerHTML = "";

    data.documents.forEach(doc => {

        let badge = "PDF";
        let badgeClass = "badge-pdf";

        let displayName = doc.filename;

        if (doc.filename.startsWith("http")) {

            badge = "URL";
            badgeClass = "badge-url";

            const url = new URL(doc.filename);

            const parts = url.pathname.split("/");

            displayName = decodeURIComponent(
                parts[parts.length - 1]
            );

            displayName = displayName.replace(/_/g, " ");

        }

        container.innerHTML += `

            <div class="document-card">

                <button
                    class="delete-btn"
                    onclick="window.deleteDocument('${doc.filename}')">

                    <i class="bi bi-trash"></i>

                </button>

                <div class="document-title">

                    <span class="document-name">

                        ${displayName}

                    </span>

                    <span class="source-badge ${badgeClass}">

                        ${badge}

                    </span>

                </div>

                <div class="document-info">

                    ${doc.chunks} Chunks

                </div>

            </div>

        `;

    });

}

window.onload = function () {

    window.loadDocuments();

}

window.deleteDocument = async function (filename) {

    const confirmDelete = confirm(
        `Delete "${filename}" ?`
    );

    if (!confirmDelete) {
        return;
    }

    const response = await fetch(

        `/documents/${encodeURIComponent(filename)}`,

        {
            method: "DELETE"
        }

    );

    const data = await response.json();

    if (data.success) {

        alert(
            `Deleted ${data.deleted_chunks} chunks`
        );

        await window.loadDocuments();

    }
}

document.getElementById("fileInput").addEventListener("change", function(){

    const label = document.getElementById("selectedFile");

    if(this.files.length){

        label.textContent = this.files[0].name;

    }else{

        label.textContent = "No file selected";

    }

});

window.uploadURL = async function () {

    const input =
        document.getElementById("urlInput");

    const url = input.value.trim();

    if (!url) {

        alert("Please enter a URL");

        return;

    }

    const response = await fetch("/upload-url", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            url: url
        })

    });

    const data = await response.json();

    if (!response.ok) {

        alert(data.detail);

        return;

    }

    document.getElementById("uploadStatus").innerHTML =
        `Indexed ${data.chunks} chunks`;

    input.value = "";

    await window.loadDocuments();

}