from conans import ConanFile, CMake, tools
import os
import shutil


class gRPCConan(ConanFile):
    name = 'grpc'
    version = '1.0.1'
    description = 'An RPC library and framework'
    url = 'https://github.com/a_teammate/conan-grpc.git'
    repo_url = 'https://github.com/grpc/grpc.git'
    license = 'MIT'
    requires = 'zlib/1.2.8@lasote/stable', 'OpenSSL/1.0.2i@lasote/stable'
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'cmake'
    # Otherwise some folders go out of the 260 chars path length
    # scope rapidly (on windows)
    short_paths = True

    def source(self):
        self.run('git clone --depth 1 --branch v{} --recursive -j{} {}'.format(self.version, tools.cpu_count(), self.repo_url))

    def build(self):
        os.chdir('grpc')
        self.run('make -j{} HAS_SYSTEM_PROTOBUF=false'.format(tools.cpu_count()))
        self.run('make install prefix={}'.format(self.package_folder))

    def package(self):
        self.copy('protoc', src='grpc/bins/opt/protobuf', dst='bin')
        self.copy('*.a', src='grpc/libs/opt/protobuf', dst='lib')

    def package_info(self):
        self.cpp_info.libs = [
                'gpr', 'grpc', 'grpc++', 'grpc_unsecure',
                'grpc++_unsecure', 'protobuf']
        if self.settings.compiler == 'Visual Studio':
            self.cpp_info.libs += ['wsock32', 'ws2_32']
        self.env_info.path.append(os.path.join(self.package_folder, 'bin'))
        self.env_info.path.append(os.path.join(self.package_folder, 'lib'))
