class AppError(Exception): # Python разрешает вызывать через raise только те объекты, которые являются исключениями
    message = "App error"

    def __init__(self, message: str | None = None):
        final_message = message or self.message
        self.message = final_message
        super().__init__(final_message) # текст ошибки попадает в системный поток ошибок (STDERR) и летит в логи(если настраивал) и консоль

# message в ините - то,что передастя при вызове UserAlreadyExists('ты даун')
# а self.message это 'User already exists"

class UserAlreadyExists(AppError):
    message = "User already exists"


class InvalidCredentials(AppError):
    message = "Invalid email or password"


class InvalidJWT(AppError):
    message = "Invalid or expired token"


class ProjectNotFound(AppError):
    message = "Project not found"


class AccessDenied(AppError):
    message = "Access denied"


class MemberExists(AppError):
    message = "Member is in a project"


class InvalidProjectMemberTarget(AppError):
    message = "InvalidProjectMemberTarget"


class UserNotFound(AppError):
    message = "UserNotFound"

class MemberNotFound(AppError):
    message = "MemberNotFound"