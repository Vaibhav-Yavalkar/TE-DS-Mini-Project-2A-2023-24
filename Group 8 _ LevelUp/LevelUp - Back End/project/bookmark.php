<?php

// Include the file that connects to the database.
include 'components/connect.php';

// Check if a user ID cookie is set.
if(isset($_COOKIE['user_id'])){
   // If set, assign it to $user_id.
   $user_id = $_COOKIE['user_id'];
}else{
   // If not set, set $user_id to an empty string and redirect to the home.php page.
   $user_id = '';
   header('location:home.php');
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
   <!-- Meta tags and title for the HTML document -->
   <meta charset="UTF-8">
   <meta http-equiv="X-UA-Compatible" content="IE=edge">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>bookmarks</title>

   <!-- Font Awesome CDN link for icons -->
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css">

   <!-- Custom CSS file link -->
   <link rel="stylesheet" href="css/style.css">

</head>
<body>

<?php include 'components/user_header.php'; ?>

<section class="courses">

   <!-- Heading for the bookmarked playlists section -->
   <h1 class="heading">bookmarked playlists</h1>

   <div class="box-container">

      <?php
         // Prepare a query to select bookmarks associated with the user.
         $select_bookmark = $conn->prepare("SELECT * FROM `bookmark` WHERE user_id = ?");
         $select_bookmark->execute([$user_id]);

         // Check if bookmarks are found.
         if($select_bookmark->rowCount() > 0){
            // Loop through each bookmark.
            while($fetch_bookmark = $select_bookmark->fetch(PDO::FETCH_ASSOC)){
               // Prepare a query to select information about the playlist associated with the bookmark.
               $select_courses = $conn->prepare("SELECT * FROM `playlist` WHERE id = ? AND status = ? ORDER BY date DESC");
               $select_courses->execute([$fetch_bookmark['playlist_id'], 'active']);

               // Check if playlist information is found.
               if($select_courses->rowCount() > 0){
                  // Loop through each playlist.
                  while($fetch_course = $select_courses->fetch(PDO::FETCH_ASSOC)){
                     // Get the course ID.
                     $course_id = $fetch_course['id'];

                     // Prepare a query to select information about the tutor associated with the playlist.
                     $select_tutor = $conn->prepare("SELECT * FROM `tutors` WHERE id = ?");
                     $select_tutor->execute([$fetch_course['tutor_id']]);
                     $fetch_tutor = $select_tutor->fetch(PDO::FETCH_ASSOC);
      ?>
      <!-- Display information about each playlist as a box -->
      <div class="box">
         <div class="tutor">
            <!-- Display tutor information -->
            <img src="uploaded_files/<?= $fetch_tutor['image']; ?>" alt="">
            <div>
               <h3><?= $fetch_tutor['name']; ?></h3>
               <span><?= $fetch_course['date']; ?></span>
            </div>
         </div>
         <!-- Display playlist thumbnail -->
         <img src="uploaded_files/<?= $fetch_course['thumb']; ?>" class="thumb" alt="">
         <!-- Display playlist title -->
         <h3 class="title"><?= $fetch_course['title']; ?></h3>
         <!-- Provide a link to view the playlist -->
         <a href="playlist.php?get_id=<?= $course_id; ?>" class="inline-btn">view playlist</a>
      </div>
      <?php
                  }
               }else{
                  // Display a message if no courses are found for the bookmark.
                  echo '<p class="empty">no courses found!</p>';
               }
            }
         }else{
            // Display a message if no bookmarks are found for the user.
            echo '<p class="empty">nothing bookmarked yet!</p>';
         }
      ?>

   </div>

</section>

<?php include 'components/footer.php'; ?>

<!-- Custom JS file link -->
<script src="js/script.js"></script>
   
</body>
</html>
