document.addEventListener("DOMContentLoaded", function() {
    // Get reference to login buttons
    const twitterLoginButton = document.getElementById("twitterLogin");
    const worldcoinLoginButton = document.getElementById("worldcoinLogin");
    const profileButtoninHome = document.getElementById("profileButtoninHome");

    // Add click event listeners
    twitterLoginButton.addEventListener("click", function(event) {
        event.preventDefault(); 
        window.location.href = "homepage.html";
    });
    profileButtoninHome.addEventListener("click", function (event) {
        event.preventDefault();
        window.location.href = "profile.html";
    });

    worldcoinLoginButton.addEventListener("click", function(event) {
        event.preventDefault(); // Prevent the default behavior of the anchor tag

        // Similar to the Twitter login button, you can handle Worldcoin login here
        // For simplicity, let's assume the login is successful
        // Redirect to another page (replace 'homepage.html' with your actual destination)
        window.location.href = "homepage.html";
    });
});
