interface UserT {
    id: string
    username?: string
    email?: string
    avatar?: string
    is_moderator: boolean
    is_admin: boolean
}

interface TagT {
    id?: string
    name: string
    posts_count?: number
}

interface PostT {
    id: string
    title: string
    body: string
    datetime: string
    user: UserT
    image?: string
    tags: Array<TagT>
}