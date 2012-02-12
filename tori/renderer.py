import  re
from    jinja2                import Environment, PackageLoader
from    tori.decorator.common import singleton
from    tori.exception        import FutureFeatureException, InvalidInput
from    tori.template         import TemplateRepository

class Renderer(object):
    def __init__(self, template_module_name):
        raise FutureFeatureException, "Need to implement."
    
    def render(self, template_path, **contexts):
        raise FutureFeatureException, "Need to implement."

class DefaultRenderer(Renderer):
    def __init__(self, template_module_name):
        # Set the name of the render.
        self.name                = template_module_name
        
        module_name_chunks       = re.split('\.', template_module_name)
        module_name              = '.'.join(module_name_chunks[:-1])
        template_sub_module_name = module_name_chunks[-1]
        
        # Set the storage of the templates.
        self.storage = Environment(loader=PackageLoader(module_name, template_sub_module_name))
    
    def render(self, template_path, **contexts):
        template = self.storage.get_template(template_path)
        return template.render(**contexts)

@singleton
class RendererService(object):
    def __init__(self, renderer_class=Renderer, repository_class=TemplateRepository):
        self._repository = repository_class(renderer_class)
    
    def register(self, renderer):
        self._repository.set(renderer)
        
        return self
    
    def render(self, renderer_name, template_path, **contexts):
        return self._repository.get(renderer_name).render(template_path, **contexts)
        