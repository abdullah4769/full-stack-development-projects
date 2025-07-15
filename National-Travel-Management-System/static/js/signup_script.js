function togglePassword() {
  let pwd = document.getElementById("password");
  let confirmPwd = document.getElementById("confirm_password");
  pwd.type = pwd.type === "password" ? "text" : "password";
  confirmPwd.type = confirmPwd.type === "password" ? "text" : "password";
}

function validateSignupForm() {
  const pwd = document.getElementById("password").value;
  const confirmPwd = document.getElementById("confirm_password").value;
  const captcha = document.getElementById("captcha").value;
  const correctCaptcha = document.getElementById("captcha_answer").value;

  const pwdRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,}$/;
  if (!pwdRegex.test(pwd)) {
    alert("Password must be at least 8 characters with uppercase, lowercase, and special character.");
    return false;
  }

  if (pwd !== confirmPwd) {
    alert("Passwords do not match.");
    return false;
  }

  if (captcha != correctCaptcha) {
    alert("Incorrect captcha answer.");
    return false;
  }

  return true;
}

window.onload = function () {
  const num1 = Math.floor(Math.random() * 10);
  const num2 = Math.floor(Math.random() * 10);
  document.getElementById("captcha-question").innerText = `${num1} + ${num2} = ?`;
  document.getElementById("captcha_answer").value = num1 + num2;
};
