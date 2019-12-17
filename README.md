Given this model, write 4 APIs: 
GET api/invitations/ List all the invitations (with pagination) 
POST api/invitations/ Create an invitation, when an invitation is created, an email to 'email' is sent
PATCH api/invitations/<id>/ Modify the invitation with the given id, if the email has been patched a new email is sent to 'email'
DELETE api/invitations/<id>/ Delete the invitation with the given id

The GET response object looks like this. 
Use standard DRF tools to paginate
```
{
    ...
    data:[
    {
        'id': <str>, 
        'createdTime': <str iso 8601 format>,
        'seconds': <int> The time since the invitation has been created in seconds
        'email': <str>,
        'used': <bool>
        'creatorEmail': <str>, 
        'creatorFullname': <str> Example: John Oliver,
    },
    ...
    ]
}
```
POST body
```
{
   'email': <str>
}
```
POST response 
An object like one in data of the GET response

PATCHable fields
```
{
    'email': <str>,
    'used': <bool>
}
```

PATCH response
The <id> object

models.py
```
class Invitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    created_time = models.DateTimeField(default=timezone.now, db_index=True)
    email = models.EmailField()
    used = models.BooleanField(default=False)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='created_invitations',
        on_delete=models.CASCADE, null=True, blank=True)
```