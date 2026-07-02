// Toggle password visibility
function togglePassword(inputId, button) {

    const input = document.getElementById(inputId);

    if (input.type === "password") {

        input.type = "text";
        button.innerText = "Hide";

    } else {

        input.type = "password";
        button.innerText = "Show";

    }

}

// Search credentials table
function searchTable() {

    const input = document.getElementById("searchInput");

    if (!input) return;

    const filter = input.value.toUpperCase();

    const table = document.getElementById("vaultTable");

    if (!table) return;

    const rows = table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) {

        const website = rows[i].cells[0].innerText.toUpperCase();
        const email = rows[i].cells[1].innerText.toUpperCase();

        rows[i].style.display =
            website.includes(filter) || email.includes(filter)
                ? ""
                : "none";
    }

}