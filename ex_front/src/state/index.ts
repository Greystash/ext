import { createGlobalState } from "react-hooks-global-state";

export interface UserT {
    username: string
    token: string
    is_moderator: boolean
    is_admin: boolean
}

interface StateT {
    showLogin: boolean
    showUsers: boolean
    showNewPost: boolean
    user: UserT | undefined
}

const initialState = {
    showLogin: false,
    showUsers: false,
    showNewPost: false,
    user: undefined,
}

const {useGlobalState} = createGlobalState<StateT>(initialState)

export {useGlobalState};
