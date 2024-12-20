document.getElementById("mashupForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = {
    singer: document.getElementById("singer").value,
    videos: document.getElementById("videos").value,
    duration: document.getElementById("duration").value,
    email: document.getElementById("email").value,
  };

  document.getElementById("message").textContent = "Processing your request...";

  try {
    const response = await fetch("http://127.0.0.1:5000/create_mashup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    const result = await response.json();
    document.getElementById("message").textContent = result.message;
  } catch (error) {
    console.error("Error:", error);
    document.getElementById("message").textContent = "Something went wrong!";
  }
});
