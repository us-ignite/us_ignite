import "classes/*.pp"

Exec {
  path => [
           "/usr/local/sbin",
           "/usr/local/bin",
           "/usr/sbin",
           "/usr/bin",
           "/sbin",
           "/bin",
           "/opt/vagrant_ruby/bin",
           "/opt/ruby/bin",
           ]
}

class dev {

  class {
    init:;
    updates: ;
    frontend: ;
  }

  host { $server_name:
    ip => '127.0.1.1',
  }

  class { "memcached":
    require => Class[init],
  }

  class { "locales":
    require => Class[init],
  }

  class { "versioning":
    require => Class[init],
  }

  class { "nodejs":
    project_path => $project_path,
  }

  class { "postsql":
    require => Class[versioning],
    username => $username,
    password => $password,
    project_name => $project_name;
  }

  class { "python":
    require => Class[postsql],
    project_path => $project_path;
  }

  class { "certificates":
    require => Class[python],
    server_name => $server_name;
  }

  class { "nginx":
    require => Class[certificates],
    server_name => $server_name,
    project_name => $project_name,
    project_path => $project_path;
  }

  class { "application":
    require => Class[nginx],
    project_path => $project_path,
    project_name => $project_name,
  }

  class { "procfile":
    require => Class[application],
    project_name => $project_name,
    project_path => $project_path;
  }

  class { "custom":
    require => Class[procfile],
    project_path => $project_path,
    project_name => $project_name;
  }

  class { "phantomjs":
    require => Class[custom],
  }

}

include dev
