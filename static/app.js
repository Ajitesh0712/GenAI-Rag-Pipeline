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

    const data = await response.json();
    console.log(data);

    let sourcesHTML = "";

    if(data.sources){

        sourcesHTML += `
        <div class="sources">

            <strong>📄 Sources</strong><br>
        `;

        data.sources.forEach(source=>{

            sourcesHTML+=`
            <span class="source-chip">

                ${source.filename}

            </span>
            `;

        });

        sourcesHTML+="</div>";

    }

    chatBox.innerHTML += `

    <div class="message assistant-message">

        <div class="message-content">

            <div class="assistant-title">

                <div class="assistant-avatar">

                    <i class="bi bi-stars"></i>

                </div>

                AI Assistant

            </div>
            <div class="mt-3">

                ${marked.parse(data.answer)}

            </div>

            ${sourcesHTML}

        </div>

    </div>

    `;

        chatBox.scrollTo({

            top:chatBox.scrollHeight,

            behavior:"smooth"

        });
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