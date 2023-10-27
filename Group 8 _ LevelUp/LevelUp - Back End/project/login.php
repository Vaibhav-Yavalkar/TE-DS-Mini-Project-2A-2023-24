<?php

// Include the file that connects to the database.
include 'components/connect.php';

// Check if a user ID cookie is set, if yes, assign it to $user_id; otherwise, set $user_id to an empty string.
if(isset($_COOKIE['user_id'])){
   $user_id = $_COOKIE['user_id'];
}else{
   $user_id = '';
}

// Check if the login form is submitted.
if(isset($_POST['submit'])){

   // Get and clean the entered email and password.
   $email = $_POST['email'];
   $email = filter_var($email, FILTER_SANITIZE_STRING);
   $pass = sha1($_POST['pass']); // Hash the password
   $pass = filter_var($pass, FILTER_SANITIZE_STRING);

   // Prepare a query to check if there's a user with the entered email and password in the database.
   $select_user = $conn->prepare("SELECT * FROM `users` WHERE email = ? AND password = ? LIMIT 1");
   
   // Execute the query with the entered email and password.
   $select_user->execute([$email, $pass]);
   
   // Fetch the user data if a match is found.
   $row = $select_user->fetch(PDO::FETCH_ASSOC);
   
   // Check if a matching user is found.
   if($select_user->rowCount() > 0){
     
     setcookie('user_id', $row['id'], time() + 60*60*24*30, '/');
     header('location:home.php');
   }else{
      // If no matching user is found, add a message saying the email or password is incorrect.
      $message[] = 'incorrect email or password!';
   }

}

?>

<!DOCTYPE html>
<html lang="en">
<head>
   <!-- Meta tags and title for the HTML document -->
   <meta charset="UTF-8">
   <meta http-equiv="X-UA-Compatible" content="IE=edge">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>Student Login</title>

   <!-- Font Awesome CDN link for icons -->
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css">

   <!-- Custom CSS file link -->
   <link rel="stylesheet" href="css/style.css">

   <!-- Inline CSS styling for the body -->
   <style>
   body {
         margin: 0;
         padding: 0;
         background: url('wallpaper.jpg') no-repeat center center fixed;
         background-size: cover;
         font-family: Arial, sans-serif;
      }

      .form-container {
         display: flex;
         justify-content: center;
         align-items: center;
         height: 100vh;
      }

      .register {
      background-color: transparent;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
      }
</style>
</head>
<body>

<!-- Section containing the login form -->
<section class="form-container">

   <!-- Login form with input fields for email and password -->
   <form action="" method="post" enctype="multipart/form-data" class="login">
      <h3>welcome back!</h3>
      <p>your email <span>*</span></p>
      <input type="email" name="email" placeholder="enter your email" maxlength="50" required class="box">
      <p>your password <span>*</span></p>
      <input type="password" name="pass" placeholder="enter your password" maxlength="20" required class="box">
      <p class="link">don't have an account? <a href="register.php">register now</a></p>
      <input type="submit" name="submit" value="login now" class="btn">
   </form>

</section>

<!-- Custom JS file link -->
<script src="js/script.js"></script>
   
</body>
</html>
