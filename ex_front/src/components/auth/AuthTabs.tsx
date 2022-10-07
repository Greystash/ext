import React from 'react';
import Tabs from 'react-bootstrap/Tabs';
import Tab from 'react-bootstrap/Tab';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';

const AuthTabs = () => {
    return (
        <Tabs
            defaultActiveKey='login'
        >
            <Tab eventKey='login' title='Login'>
                <LoginForm />
            </Tab>

            <Tab eventKey='register' title='Register'>
                <RegisterForm />
            </Tab>
        </Tabs>
    )
}

export default AuthTabs;