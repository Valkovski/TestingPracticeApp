function bindAutoSubmitQuantity() {
  document.querySelectorAll("[data-cart-qty]").forEach((input) => {
    input.addEventListener("change", () => {
      const form = input.closest("form");
      if (form) form.requestSubmit();
    });
  });
}

async function handleCartFormSubmit(event) {
  const form = event.target;
  if (!(form instanceof HTMLFormElement)) return;
  if (!form.dataset.cartAction) return;

  event.preventDefault();
  const submitButton = form.querySelector("button[type='submit']");
  if (submitButton) submitButton.disabled = true;

  try {
    const response = await fetch(form.action, {
      method: (form.method || "POST").toUpperCase(),
      body: new FormData(form),
      redirect: "follow",
    });

    window.location.href = response.url || window.location.href;
  } catch {
    window.location.reload();
  }
}

document.addEventListener("submit", handleCartFormSubmit);
document.addEventListener("DOMContentLoaded", bindAutoSubmitQuantity);

