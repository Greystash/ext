import React, { useEffect, useState } from 'react';
import Modal from 'react-bootstrap/Modal';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import { useGlobalState } from '../../state';
import api from '../../api';


const UsersModal = () => {
    const [showUsers, setShowUsers] = useGlobalState('showUsers')
    const [users, setUsers] = useState<Array<UserT>>([])

    useEffect(() => {
        if (showUsers) {
            api.get('auth/get-users/').then(res => {
                setUsers(res.data)
            })
        }
    }, [showUsers])

    const handleUserChange = (user: UserT) => {
        api.post('auth/update-groups/', { user_id: user.id, is_moderator: !user.is_moderator })
    }

    return (
        <Modal
            show={showUsers}
            onHide={() => { setShowUsers(false) }}
        >
            {users.map(user => <Card key={user.id}>
                <Card.Body>
                    <Card.Text>
                        {`${user.username ? user.username : user.email} ${user.is_moderator ? 'is a moderator' : 'is not a moderator'}`}
                    </Card.Text>
                    <Button
                        variant={user.is_moderator ? 'outline-danger' : 'outline-success'}
                        size='sm'
                        onClick={() => handleUserChange(user)}
                    >{user.is_moderator ? 'Remove from moderators' : 'Add to moderators'}</Button>
                </Card.Body>
            </Card>)}
        </Modal>
    )
}

export default UsersModal;