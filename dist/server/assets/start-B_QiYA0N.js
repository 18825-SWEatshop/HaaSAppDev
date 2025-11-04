import { createSerializationAdapter } from "@tanstack/react-router";
const createMiddleware = (options, __opts) => {
  const resolvedOptions = {
    type: "request",
    ...__opts || options
  };
  return {
    options: resolvedOptions,
    middleware: (middleware) => {
      return createMiddleware(
        {},
        Object.assign(resolvedOptions, { middleware })
      );
    },
    inputValidator: (inputValidator) => {
      return createMiddleware(
        {},
        Object.assign(resolvedOptions, { inputValidator })
      );
    },
    client: (client) => {
      return createMiddleware(
        {},
        Object.assign(resolvedOptions, { client })
      );
    },
    server: (server) => {
      return createMiddleware(
        {},
        Object.assign(resolvedOptions, { server })
      );
    }
  };
};
const createStart = (getOptions) => {
  return {
    getOptions: async () => {
      const options = await getOptions();
      return options;
    },
    createMiddleware
  };
};
const serverMw = createMiddleware().server(({
  next,
  context
}) => {
  context.fromFetch;
  const nonce = Math.random().toString(16).slice(2, 10);
  console.log("nonce", nonce);
  return next({
    context: {
      fromServerMw: true,
      nonce
    }
  });
});
const fnMw = createMiddleware({
  type: "function"
}).middleware([serverMw]).server(({
  next,
  context
}) => {
  context.fromFetch;
  return next({
    context: {
      fromFnMw: true
    }
  });
});
const serializeClass = createSerializationAdapter({
  key: "Test",
  test: (v) => v instanceof Test,
  toSerializable: (v) => v.test,
  fromSerializable: (v) => new Test(v)
});
class Test {
  constructor(test) {
    this.test = test;
  }
  init() {
    return this.test;
  }
}
const startInstance = createStart(() => {
  return {
    defaultSsr: true,
    serializationAdapters: [serializeClass]
  };
});
export {
  Test,
  fnMw,
  serverMw,
  startInstance
};
