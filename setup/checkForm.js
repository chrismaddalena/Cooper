function checkForm(form)
{
  var results = ["Password stats:"];
  var pass = form.pwd.value;
  var user = form.username.value;
  var isUsernameInPass = pass.indexOf(user);
  var passIsUser = 0;
  var bad = 0;
  results.push(form.pwd.value.length + " characters"); //Count password length and record
  if(pass == user) {
    results.push("[!] Password same as username");
    passIsUer = 1;
  }
  if(isUsernameInPass > -1 & passIsUser == 0) {
    results.push("[!] Username is in password");
  }
  re = /[0-9]/;
  if(!re.test(form.pwd.value)) {
   results.push("[!] Contains no numbers");
  }
  re = /[a-z]/;
  if(!re.test(form.pwd.value)) {
    results.push("[!] All uppercase");
    bad = 1;
  }
  re = /[A-Z]/;
  if(!re.test(form.pwd.value)) {
    results.push("[!] All lowercase");
    bad = 1;
  }
  re = /^[a-zA-Z]+$/;
  if(re.test(form.pwd.value) & bad == 0) {
    results.push("[:)] Mixed case");
  }
  re = /[$&+,:;=?@#|'<>.^*()%!\/\\-]/;
  if(!re.test(form.pwd.value)) {
    results.push("[!] No special characters");
  }
  results.push("Username: " + form.username.value);
  form.pwd.value = "Password: REDACTED";
  results.push(form.pwd.value);
  alert(results.join('\n'));
}