const usernameArea = document.querySelector('#usernameField')
 const usernamefeedBackArea = document.querySelector('.usernameinvalid-feedback')
 const submitBtn = document.querySelector('#submit-btn')

  //username validation check
  usernameArea.addEventListener("keyup",(e)=>{
    console.log('hello Iam working')
    const usernameVal = e.target.value;

    usernameArea.classList.remove("is-invalid");
    usernamefeedBackArea.style.display = "none";

          if (usernameVal.length>0){
           //var url =
            fetch ('/username-valid/', {
             method: "POST",
              body: JSON.stringify({ username : usernameVal }),
             })
            .then((res)=>{
              return res.json();
             })
            .then((data)=>{
              console.log('data:', data)
              if(data.username_error){
               console.log(data.username_error)
              usernameArea.classList.add("is-invalid");
              usernamefeedBackArea.style.display = "block";
              usernamefeedBackArea.innerHTML = `${data.username_error}`
              submitBtn.disabled = true;
            }else{
              submitBtn.removeAttribute("disabled");
            }
             })
           }
     })

 //email validation check
 const emailfieldArea = document.querySelector('#Emailfield')
 const emailfeedBackArea = document.querySelector('.emailinvalid-feedback')

 emailfieldArea.addEventListener("keyup",(e)=>{
   console.log('hello Iam working')
   const emailVal = e.target.value;

   emailfieldArea.classList.remove("is-invalid");
   emailfeedBackArea.style.display = "none";

   if (emailVal.length>0){
    //var url =
     fetch ('/email-validation/', {
       method: "POST",
       body: JSON.stringify({ email : emailVal }),
     })
     .then((res)=>{
       return res.json();
     })
     .then((data)=>{
       console.log('data:', data)
       if(data.email_error){
         console.log(data.email_error)
         submitBtn.disabled =true;
         emailfieldArea.classList.add("is-invalid");
        emailfeedBackArea.style.display = "block";
        emailfeedBackArea.innerHTML = `${data.email_error}`
      }{
        submitBtn.removeAttribute("disabled");
      }
     })
   }
 })
