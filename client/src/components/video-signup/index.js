import React, { Component } from 'react';
import { Button, Container, Divider } from 'semantic-ui-react';
import { ToastContainer, toast } from 'react-toastify';
import '../../../../css/main.css'

class VideoSignUp extends Component {
  constructor(props){
  	super(props)
    this.state = {
      'qty': 1
    }
  }

  componentWillUnmount(){
    console.log('desmontando videosignup')
  	let xhr = new XMLHttpRequest();
    xhr.open('GET', '/video_stream?fd=false');
    xhr.send();
  }

  train_pic = () =>{
    // console.log('train_pic', this.state.qty)
    let uid = this.props.uid;
    let data = new FormData();
    data.append('qty', this.state.qty);
    data.append('uid', uid);
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/train_pic');
    xhr.onreadystatechange = () => {
      if (xhr.readyState == 4) {
        if (xhr.status == 200) {
          this.setState(prevState => {
            return {qty: prevState.qty+1}
          });
          if (this.state.qty == 5) {
            this.props.handleReg('home')
          }else{
            toast.success("Rostro capturado exitosamente !", {
              position: toast.POSITION.TOP_RIGHT
            });
          }
        }
      }
    };
    xhr.send(data);
  }


  render() {
    let container;
    return (
      <Container style={{background: 'none'}}>
        <img id="videofield" className="video" src='/video_stream?fd=true' />
        <Divider horizontal/>
        <Button id="train_pic" content='Capturar Rostro!' onClick={this.train_pic.bind(this)} />
        <ToastContainer autoClose={1500}/>
      </Container>
    )
  }
}

export default VideoSignUp;

