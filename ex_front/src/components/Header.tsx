import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import { useGlobalState } from '../state';
import api from '../api';

const Header = () => {
    const [_, setshowLogin] = useGlobalState('showLogin');
    const [showUsers, setshowUsers] = useGlobalState('showUsers');
    const [showNewPost, setShowNewPost] = useGlobalState('showNewPost')
    const [user, setUser] = useGlobalState('user');

    const logout = () => {
        api.post('auth/logout/').then(res => { console.log(res) })
        delete api.defaults.headers.common['Authorization']
        setUser(undefined)
    }

    return (
        <Navbar >
            <Container fluid={true}>
                <Navbar.Brand>
                    News
                </Navbar.Brand>
                <Button
                    size='lg'
                    variant='outline-info'
                    hidden={user !== undefined}
                    onClick={() => { setshowLogin(true) }}
                >Login</Button>
                <h5 hidden={user === undefined}>Hello, {user?.username}</h5>
                <ButtonGroup hidden={user === undefined}>
                    <Button
                        size='lg'
                        variant='outline-primary'
                        hidden={!user?.is_moderator}
                        onClick={() => { setShowNewPost(true) }}
                    >
                        New post
                    </Button>
                    <Button
                        size='lg'
                        variant='outline-warning'
                        hidden={!user?.is_admin}
                        onClick={() => { setshowUsers(true) }}
                    >
                        Users
                    </Button>
                    <Button
                        size='lg'
                        variant='outline-danger'
                        onClick={logout}
                    >
                        Logout
                    </Button>
                </ButtonGroup>
            </Container>
        </Navbar>
    )
}

export default Header;