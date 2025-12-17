async function rewriteNews() {
const content = document.getElementById("content").value;
const location = document.getElementById("location").value;
const mode = document.getElementById("mode").value;


const formData = new FormData();
formData.append("content", content);
formData.append("location", location);
formData.append("mode", mode);


const res = await fetch("/rewrite", { method: "POST", body: formData });
const data = await res.json();


document.getElementById("output").innerText = data.output;
}
