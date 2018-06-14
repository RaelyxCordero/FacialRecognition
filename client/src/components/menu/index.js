import React, { Component } from 'react'
import { Input, Label, Menu } from 'semantic-ui-react'

export default class MenuPrincipal extends Component {
  state = { activeItem: '' }

  handleItemClick = (e, { name }) => {
    this.setState({ activeItem: name })
    this.props.handleMenuClick(name)
  }

  render() {
    const { activeItem } = this.state

    return (
      <Menu size='large' vertical inverted>
        <Menu.Item name='menu' align='center'>
          Menu
        </Menu.Item>
         <Menu.Item name='home' active={activeItem === 'home'} onClick={this.handleItemClick}>
          Inicio
        </Menu.Item>
        <Menu.Item name='signin' active={activeItem === 'signin'} onClick={this.handleItemClick}>
          Iniciar Sesión
        </Menu.Item>

        <Menu.Item name='signup' active={activeItem === 'spam'} onClick={this.handleItemClick}>
          Registrate
        </Menu.Item>
      </Menu>
    )
  }
}