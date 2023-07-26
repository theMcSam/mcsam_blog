from fastapi import HTTPException, status


class IncorrectUsernameOrPassword(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Incorrect username or password."


class DuplicateUsernames(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Duplicate usernames not allowed."


class DuplicateEmails(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Duplicate email not allowed."


class UnauthorizedUser(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "You are not authorized to perform this action."


class PostNotFound(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Post not found."


class DeletedSuccessfully(HTTPException):
    status_code = status.HTTP_204_NO_CONTENT
    detail = "Deleted successfully."
