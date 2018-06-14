import React, { Component } from 'react';
import { Button, Container, Segment, Form } from 'semantic-ui-react';
import '../../../../css/main.css'

class VideoSignIn extends Component {
  constructor(props){
  	super(props)
    this.state = {
      status: 0,
      name: '',
      uid: 0,
      next: false,
      password: ''
    }
  }
  identPic = () => {
    this.setState({status: 0})
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/ident_pic');
    xhr.onreadystatechange = () => {
      if (xhr.readyState == 4) {
        if (xhr.status == 200) {
            let rs = JSON.parse(xhr.responseText);
            this.setState({status: 200, name: rs.name, uid: rs.uid})
            console.log(this.state.name)
        }
      }
    };
    xhr.send();
  }

  askPass = () => {
    this.setState({next: true})
  }

  handleChange = (e, { name, value }) => this.setState({ [name]: value })

  handleLoginClick = () => {
    console.log(this.state.password, this.state.uid)
    var data = new FormData();
    data.append('password', this.state.password);
    data.append('uid', this.state.uid);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/login')
    xhr.onreadystatechange = () => {
      if(xhr.readyState == 4) {
        if(xhr.status == 200){
          let rs = JSON.parse(xhr.responseText);
          if(rs.name){
            // cambiar ruta
            this.props.handleLogin(true, rs.name)
          }
        }
      }
    }
    xhr.send(data);
  }

  componentDidMount() {
    setTimeout(this.identPic,3000)
  }
  componentWillUnmount(){
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/video_stream?fd=false');
    xhr.send();
  }

  render() {
    var tryButton = ''
    var nextButton = ''
    var nextContainer = ''
    if(this.state.next){
      nextContainer = <Segment inverted><Form inverted><Form.Input name='password' value={this.state.password} onChange={this.handleChange} fluid required  placeholder='Contraseña' type='password' /></Form><Button type='submit' name='login' onClick={this.handleLoginClick}>Iniciar Sesión</Button> </Segment>
    }else{
      if(this.state.status == 200){
        tryButton = <Button id="ident_pic" content='Me equivoque? Intentalo de nuevo!' onClick={this.identPic.bind(this)} />
        if(this.state.name != '' && this.state.name){
          nextButton = <Button id="next" content='Siguiente' onClick={this.askPass} />
        }
      }
    }
    return (
      <Container style={{background: 'none'}}>
        <img id="videofield" className="video" src='/video_stream?fd=true' />
        <br/>
        {nextButton}
        {tryButton}
        {nextContainer}
      </Container>
    )
  }
}

export default VideoSignIn;

