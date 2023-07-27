from fastapi import HTTPException, status


class IncorrectUsernameOrPassword(HTTPException):
    pass


class DuplicateUsernames(HTTPException):
    pass


class DuplicateEmails(HTTPException):
    pass


class UnauthorizedUser(HTTPException):
    pass


class PostNotFound(HTTPException):
    pass


class DeletedSuccessfully(HTTPException):
    pass
