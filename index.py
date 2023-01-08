"""
@authors: moise berthe, lina belhadj
"""
import cgi
print("Content-type: text/html; charset=utf-8")


html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Moteur de recherche</title>
</head>
<body>
    <style>
        body{
            margin: 0;
            padding: 0;
        }
        .container{
            height: 100vh;
            position: relative;
        }
        .content{
            position: absolute;
            top: 50%;
            left: 50%;
            min-width: 480px;
            max-width: 720px;
            transform: translate(-50%, -50%);
        }
        .main-title{
            text-align: center;
        }

        .main-title .title{
            margin: 0;
            text-align: center;
            text-transform: uppercase;
            color: #103456;
            font-size: 48px;
            font-weight: bolder;
            margin-bottom: 16px;
            letter-spacing: 5px;
            text-shadow: 1px 1px 3px black;
        }

        .form-elt {
            margin-bottom: 16px;
        }
        .form-elt .search{
            padding: 16px;
            border: 1px solid #e4e4e4;
            border-radius: 32px;
            width: 100%;
            outline: none;
            font-size: 16px;
        }
        .form-elt .search:focus{
            box-shadow: 0 1px 6px rgb(32 33 36 / 28%);
        }
        .submit{
            text-align: center;
        }
        .submiter{
            background-color: #103456;
            border: 1px solid #103456;
            border-radius: 32px;
            padding: 16px;
            font-size: 16px;
            color: #fff;
            cursor: pointer;
        }
        .submiter:hover{
            background-color: #fff;
            color: #103456;
        }
    </style>
    <div class="container">
        <div class="content">
            <div class="main-title">
                <h2 class="title">Search engine</h2>
            </div>
            <form action="web-search.py" method="get" class="form">
                <div class="form-elt">
                    <input type="text" name="query" id="query" class="search" placeholder="Rechercher">
                </div>
                <div class="submit">
                    <button type="submit" class="submiter" id="submiter">Rechercher</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
"""
print(html)