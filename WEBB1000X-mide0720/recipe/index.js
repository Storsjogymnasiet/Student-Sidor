const listItems = document.querySelectorAll("section#maträtter > article > h2");
const maträtter = document.getElementById('maträtter');
const searchbox = document.getElementById("search");
const nothingHereText = document.getElementById("nothing-here");
const popup = {
    body: document.getElementById("popup"),
    iframe: document.getElementById("popup-iframe"),
    closer: document.getElementById("popup-close"),
    closeFunction: () => {
        popup.body.style.visibility = "hidden";
        const url = new URL(window.location);
        url.hash = "";
        history.replaceState(null, null, url);
    }
};

function applyFilter(rawTerm) {
    const searchTerm = rawTerm.trim().toLowerCase();
    let count = 0;

    listItems.forEach(item => {
        item.parentElement.style.display = 'revert';
        if (!item.innerText.toLowerCase().includes(searchTerm)) {
            item.parentElement.style.display = 'none';
        } else {
            count++;
        }
    });

    if (count === 0) {
        maträtter.style.gridTemplateColumns = '1fr';
        nothingHereText.style.display = 'block';
    } else if (count < 3) {
        maträtter.style.gridTemplateColumns = `repeat(${count}, auto)`;
        nothingHereText.style.display = 'none';
    } else {
        maträtter.style.gridTemplateColumns = 'repeat(3, auto)';
        nothingHereText.style.display = 'none';
    }
}

function filterByName(event) {
    const rawTerm = event.target.value;
    applyFilter(rawTerm);

    const url = new URL(window.location);
    if (rawTerm.trim()) {
        url.searchParams.set("q", rawTerm.trim());
    } else {
        url.searchParams.delete("q");
    }


    window.history.replaceState({}, "", url);
}

document.addEventListener("keydown", e => {
    if (e.ctrlKey && e.key === "k") {
        searchbox.focus();
        e.preventDefault();
    }
});

(() => {

    const params = new URLSearchParams(window.location.search);
    const initialQuery = params.get("q");
    if (initialQuery) {
        searchbox.value = initialQuery;
        applyFilter(initialQuery);
    }

    popup.closer.addEventListener("click", popup.closeFunction);
    //window.location.body.addEventListener("click", popup.closeFunction);

    document.querySelectorAll("section#maträtter > article").forEach(a => {
        a.addEventListener("click", () => {
            popup.body.style.visibility = "visible";
            popup.iframe.src = "./recipes/" + a.dataset.href + ".html";
            window.location.hash = `#${a.dataset.href.replace(/\.html$/g, "")}`;
        });
    });

    const hash = window.location.hash.slice(1);
    if (hash.length > 0) {
        popup.body.style.visibility = "visible";
        popup.iframe.src = "./recipes/" + hash + ".html";
    }
})();