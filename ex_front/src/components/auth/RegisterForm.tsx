import React, { useState, useEffect } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import api from '../../api';
import { useGlobalState, UserT } from '../../state';


const RegisterForm = () => {
    const [user, setUser] = useGlobalState('user')
    const [data, setData] = useState({
        email: '',
        username: '',
        password: ''
    });


    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const valueName = e.target.name
        const value = e.target.value
        setData({ ...data, [valueName]: value })
    }

    const handleSubmit = (e: React.SyntheticEvent) => {
        e.preventDefault()
        api.post('auth/register/', data)
            .then(res => {
                const newUser: UserT = {
                    token: res.data.token,
                    username: res.data.user.username ? res.data.user.username : res.data.user.email,
                    is_moderator: res.data.user.is_moderator,
                    is_admin: res.data.user.is_admin
                };
                setUser(newUser);
                api.defaults.headers.common['Authorization'] = `Token ${newUser.token}`
            })
            .catch(e => { console.log(e) })
    }


    return (
        <Form
            onSubmit={handleSubmit}
        >
            <Form.Group className="mb-3" >
                <Form.Label>Username</Form.Label>
                <Form.Control type="text"
                    placeholder="Enter username"
                    name='username'
                    onChange={handleChange} />
                <Form.Text className="text-muted">
                    Email OR username must be provided.
                </Form.Text>
            </Form.Group>

            <Form.Group className="mb-3" >
                <Form.Label>Email</Form.Label>
                <Form.Control type="text"
                    placeholder="Enter email"
                    name='email'
                    onChange={handleChange} />
                <Form.Text className="text-muted">
                    Email OR username must be provided.
                </Form.Text>
            </Form.Group>

            <Form.Group className="mb-3">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password"
                    placeholder="Password"
                    name='password'
                    onChange={handleChange}
                />
            </Form.Group>
            <Button
                variant="primary"
                type="submit">
                Submit
            </Button>
        </Form>
    )
}

export default RegisterForm;