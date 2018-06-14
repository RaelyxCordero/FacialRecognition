import React, { Component } from 'react'
import { Button, Form, Segment, Checkbox } from 'semantic-ui-react'

export default class RegForm extends Component {
  constructor(props){
    super(props);
    this.state = { name: '', password: '', tyc: false, uid: '' }
    // this.handleDataUser = this.handleDataUser.bind(this);
  }

  handleChange = (e, { name, value }) => this.setState({ [name]: value })
  toggle = () => this.setState({ tyc: !this.state.tyc })

  handleSubmitClick = (e, { name }) => {
    if(this.state.name && 
      this.state.password && 
      this.state.tyc &&
      this.state.name.replace(/\s/g, '').length &&
      this.state.password.replace(/\s/g, '').length){
      /*REGISTRAR USUARIO Y ACTIVAR CAMARA*/
      var data = new FormData();
      data.append('name', this.state.name);
      data.append('password', this.state.password);

      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/reg_user', true);
      xhr.onreadystatechange = () => {
          if (xhr.readyState == 4) {
              if (xhr.status == 200) {
                  let uid = JSON.parse(xhr.responseText).id;
                  this.setState({ uid: uid })
                  this.props.handleDataUser(uid)
                  // this.props.handleMenuClick('signup_next')
              }
          }
      };
      xhr.send(data);
    }
    
  }
  render(){
    return(
      <Segment inverted>
        <Form inverted>
          <Form.Group widths='equal'>
            <Form.Input name='name' value={this.state.name} onChange={this.handleChange} fluid required label='Nombre completo' placeholder='Nombre' />
            <Form.Input name='password' value={this.state.password} onChange={this.handleChange} fluid required label='Contraseña' placeholder='Contraseña' type='password' />
          </Form.Group>
          <Checkbox name='tyc' checked={this.state.tyc} onChange={this.toggle} label='Acepto terminos y condiciones' />
          <br/>
        </Form>
        <Button type='submit' name='signup_next' onClick={this.handleSubmitClick}>Siguiente</Button>
      </Segment>
    )
  }
}