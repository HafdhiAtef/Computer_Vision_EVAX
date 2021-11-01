import './App.css';
import React, { useRef, useState, useEffect } from 'react';
import axios from "axios";

function App() {
  const API_URL= "http://127.0.0.1:5000/";
  const videoRef = useRef(null);
  const photoRef = useRef(null);
  const [hasPhoto, setHasPhoto] = useState(false);
  const getVideo = () => {
    navigator.mediaDevices.getUserMedia({
      video: { width: 1920, height: 1080 }
    }).then(stream => {
      let video = videoRef.current;
      video.srcObject = stream;
      video.play();
    }).catch(err => {
      console.error(err);
    })
  };



  async function uploadImage (file)   {
    var formData = new FormData();
    formData.append("photo", file);
  
    return await axios.post(API_URL, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  }


  const takePhoto = () => {
    const width = 414;
    const height = width / (16 / 9);
    let video = videoRef.current;
    let photo = photoRef.current;

    photo.width = width;
    photo.height = height;



    let ctx = photo.getContext('2d');

    ctx.drawImage(video, 0, 0, width, height);
    setHasPhoto(true);
    var canvas = document.querySelector('#canvasssss');
    var cccccccccccc = canvas.toDataURL("image/jpeg", 1.0);
    try {
      uploadImage(cccccccccccc);
    } catch (error) {
      console.log(error)
    }
    
  }
  const closePhoto = () => {
    let photo = photoRef.current;
    let ctx = photo.getContext('2d');

    ctx.clearRect(0, 0, photo.width, photo.height);

    setHasPhoto(false);
  }


  useEffect(() => {
    getVideo();
  }, [videoRef]);

  return (
    <div className="App">
      <div className="camera">
        <video ref={videoRef}>

        </video>
        <button onClick={takePhoto}>SNAP!</button>
      </div>
      <div className={"result " + (hasPhoto ? 'hasPhoto' : '')}>
        <canvas id="canvasssss" ref={photoRef}></canvas>

        <button onClick={closePhoto}> CLOSE!</button>
      </div>
    </div>
  );
}

export default App;
