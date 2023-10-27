<?php

// Include the file that connects to the database.
include 'components/connect.php';

// Check if a user ID cookie is set; if yes, assign it to $user_id; otherwise, set $user_id to an empty string.
if(isset($_COOKIE['user_id'])){
   $user_id = $_COOKIE['user_id'];
}else{
   $user_id = '';
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
   <!-- Meta tags and title for the HTML document -->
   <meta charset="UTF-8">
   <meta http-equiv="X-UA-Compatible" content="IE=edge">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>LevelUp - about</title>

   <!-- Font Awesome CDN link for icons -->
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css">

   <!-- Custom CSS file link -->
   <link rel="stylesheet" href="css/style.css">

</head>
<body>

<?php include 'components/user_header.php'; ?>

<!-- about section starts  -->

<section class="about">

   <div class="row">

      <div class="image">
         <!-- Image illustrating the section -->
         <img src="images/about-img.svg" alt="">
      </div>

      <div class="content">
         <!-- Heading for the section -->
         <h3>why choose us?</h3>
         <!-- Paragraph explaining why to choose the platform -->
         <p>Learning is pivotal for a student's success in academics and life. The Digital Age is deeply shaping the way students learn and will also determine their future prospects. At LevelUp, we encourage students to embrace this fast, changing world and make them ready for tomorrow by being their constant learning partner. We craft learning journeys for every student that address their unique needs. We believe in the power of one-to-one learning that addresses every child's learning needs, allows students to be holistically involved in their education and be active, lifelong learners.</p>
         <!-- Button linking to courses -->
         <a href="courses.html" class="inline-btn">our courses</a>
      </div>

   </div>

   <div class="box-container">

      <!-- Statistics boxes highlighting key numbers -->
      <div class="box">
         <i class="fas fa-graduation-cap"></i>
         <div>
            <!-- Number of online courses -->
            <h3>+1k</h3>
            <span>online courses</span>
         </div>
      </div>

      <div class="box">
         <i class="fas fa-user-graduate"></i>
         <div>
            <!-- Number of brilliant students -->
            <h3>+25k</h3>
            <span>brilliant students</span>
         </div>
      </div>

      <div class="box">
         <i class="fas fa-chalkboard-user"></i>
         <div>
            <!-- Number of expert teachers -->
            <h3>+5k</h3>
            <span>expert teachers</span>
         </div>
      </div>

      <div class="box">
         <i class="fas fa-briefcase"></i>
         <div>
            <!-- Job placement percentage -->
            <h3>100%</h3>
            <span>job placement</span>
         </div>
      </div>

   </div>

</section>

<!-- about section ends -->

<!-- reviews section starts  -->

<section class="reviews">

   <!-- Heading for the reviews section -->
   <h1 class="heading">student's reviews</h1>

   <div class="box-container">

      <!-- Review boxes with user feedback -->
      <div class="box">
         <!-- Review content -->
         <p>Great mentors, visual learning, and unique teaching methods are what excite Mannat of class 11. She can watch lessons anywhere and anytime, and the interactive learning process excites her very much.</p>
         <!-- User details with an image and star rating -->
         <div class="user">
            <img src="images/pic-2.jpg" alt="">
            <div>
               <!-- User's name -->
               <h3>Mannat Khan</h3>
               <!-- Star rating for the review -->
               <div class="stars">
                  <i class="fas fa-star"></i>
                  <i class="fas fa-star"></i>
                  <i class="fas fa-star"></i>
                  <i class="fas fa-star"></i>
                  <i class="fas fa-star-half-alt"></i>
               </div>
            </div>
         </div>
      </div>

      <!-- Repeat similar structure for other reviews -->

   </div>

</section>

<!-- reviews section ends -->

<?php include 'components/footer.php'; ?>

<!-- Custom JS file link -->
<script src="js/script.js"></script>
   
</body>
</html>
