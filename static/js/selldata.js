var loadFile = function (event) {
      var output = document.getElementById('output');
      output.src = URL.createObjectURL(event.target.files[0]);
      output.onload = function () {
        URL.revokeObjectURL(output.src)
      }
    };

    var firebaseConfig = {
      "apiKey": "AIzaSyCbUntIsZducvP0bpT9O6kLLn53o2Q--Ak",
      "authDomain": "semester-6-f45fb.firebaseapp.com",
      "databaseURL": "https://semester-6-f45fb-default-rtdb.firebaseio.com",
      "storageBucket": "semester-6-f45fb.appspot.com",
      "messagingSenderId": "17109620482",
    }
    firebase.initializeApp(firebaseConfig);


    function uploadimage() {
      var storage = firebase.storage();
      var file = document.getElementById("files").files[0];
      var storageRef = storage.ref();
      var thisref = storageRef.child(file.name).put(file);
      thisref.on('state_changed', function (snapshot) {
        console.log("file uplaoded succesfully");
      },
        function (error) {
        },
        function () {
          // Upload completed successfully, now we can get the download URL
          var downloadURL = thisref.snapshot.downloadURL;
          console.log("got url");
          document.getElementById("url").value = downloadURL;
          alert("file uploaded successfully");
        });

    }