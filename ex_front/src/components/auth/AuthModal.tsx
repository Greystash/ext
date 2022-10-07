import React from 'react';
import Modal from 'react-bootstrap/Modal';
import { useGlobalState } from '../../state';
import AuthTabs from './AuthTabs';


const AuthModal = () => {
    const [showLogin, setshowLogin] = useGlobalState('showLogin');

    return (
        <Modal
            show={showLogin}
            onHide={() => { setshowLogin(false) }}>
            <Modal.Header>
                <Modal.Title>
                    Login or register
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <AuthTabs />
            </Modal.Body>
        </Modal>
    )
}

export default AuthModal;
