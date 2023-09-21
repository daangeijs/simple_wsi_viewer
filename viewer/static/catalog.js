document.addEventListener("DOMContentLoaded", function () {
    const lazyImages = document.querySelectorAll(".lazyload");
    new LazyLoad(lazyImages);

    function checkIndexingStatus() {
        fetch('/check_indexing_status/')
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                if (data.finished) {
                    document.getElementById("notification").style.display = "none";
                    clearInterval(pollingInterval);
                }
            })
            .catch(error => {
                console.error("There was a problem with the fetch operation:", error.message);
            });
    }

    let pollingInterval;
    if (document.getElementById("notification").style.display === "block") {
        pollingInterval = setInterval(checkIndexingStatus, 5000);  // Check every 5 seconds
    }
});
