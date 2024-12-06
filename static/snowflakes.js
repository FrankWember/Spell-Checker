const createSnowflake = () => {
    const snowflake = document.createElement("div");
    snowflake.classList.add("snowflake");
    snowflake.textContent = "❄️";

    snowflake.style.left = `${Math.random() * 100}vw`;
    snowflake.style.animationDuration = `${3 + Math.random() * 5}s`; 
    snowflake.style.opacity = Math.random();
    snowflake.style.fontSize = `${10 + Math.random() * 40}px`;

    document.body.appendChild(snowflake);

    setTimeout(() => {
        snowflake.remove();
    }, 8000); 
};

setInterval(createSnowflake, 200);
