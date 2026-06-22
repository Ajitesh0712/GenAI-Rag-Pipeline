async function uploadFile() {

    const fileInput =
        document.getElementById("fileInput");

    if (fileInput.files.length === 0) {
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

    document.getElementById(
        "uploadResult"
    ).innerHTML =
        `<p>${data.filename}</p>`;
}